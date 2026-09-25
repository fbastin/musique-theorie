\version "2.24.3"
%% Fichier produit par outils/generer.py — ne pas modifier à la main.
\paper {
  indent = 0
  ragged-right = ##t
  top-margin = 1\mm
  bottom-margin = 1\mm
  left-margin = 1\mm
  right-margin = 1\mm
  oddHeaderMarkup = ##f
  evenHeaderMarkup = ##f
  oddFooterMarkup = ##f
  evenFooterMarkup = ##f
  bookTitleMarkup = ##f
  scoreTitleMarkup = ##f
}
#(define (armure-nouveau-signe pas couleur)
   (lambda (grob)
     (let* ((alist (ly:grob-property grob 'alteration-alist))
            (reste (filter (lambda (e) (not (eqv? (car e) pas))) alist))
            (tout (stencil-with-color
                   (ly:key-signature-interface::print grob) couleur)))
       (if (null? reste)
           tout
           (begin
             (ly:grob-set-property! grob 'alteration-alist reste)
             (let ((ancien (ly:key-signature-interface::print grob)))
               (ly:grob-set-property! grob 'alteration-alist alist)
               (ly:stencil-add tout ancien)))))))

\score {
  \new Staff \with {
    \consists "Horizontal_bracket_engraver"
    \override HorizontalBracket.direction = #DOWN
    \override HorizontalBracketText.font-size = #-3
    \override HorizontalBracketText.font-shape = #'italic
  } {
    %% Sans barres de mesure, une altération reste en vigueur jusqu'à la fin de
    %% la figure : le ré bémol du tétracorde phrygien n'était pas réimprimé sur
    %% la ligne du tétracorde harmonique, qui se lisait donc « do ré mi fa » —
    %% l'orthographe du tétracorde majeur. Même effet sur la mineure mélodique,
    %% dont le sol dièse disparaissait et qui se lisait en mode dorien.
    %% `forget` réimprime chaque altération par rapport à l'armure, sans
    %% mémoire de ce qui précède : chaque ligne se lit alors seule.
    \accidentalStyle forget
    \clef treble
    \omit Staff.TimeSignature
    \cadenzaOn
    \set Staff.printKeyCancellation = ##f
    \set Staff.explicitKeySignatureVisibility = #end-of-line-invisible
    \set Staff.instrumentName = \markup \small "do"
    \key c \major
    \once \override Staff.HorizontalBracketText.text = "inférieur"
    c'\startGroup d' e' f'\stopGroup
    \once \override Staff.HorizontalBracketText.text = "supérieur"
    g'\startGroup a' b' c''\stopGroup
    \bar "" \break
    \set Staff.shortInstrumentName = \markup \small "sol"
    \once \override Staff.KeySignature.stencil = #(armure-nouveau-signe 3 (rgb-color 0.588 0.157 0.118))
    \key g \major
    \once \override Staff.HorizontalBracketText.text = "inférieur"
    g'\startGroup a' b' c''\stopGroup
    \once \override Staff.HorizontalBracketText.text = "supérieur"
    d''\startGroup e'' \tweak color #(rgb-color 0.588 0.157 0.118) \tweak Stem.color #(rgb-color 0.588 0.157 0.118) fis'' g''\stopGroup
    \bar "" \break
    \set Staff.shortInstrumentName = \markup \small "ré"
    \once \override Staff.KeySignature.stencil = #(armure-nouveau-signe 0 (rgb-color 0.588 0.157 0.118))
    \key d \major
    \once \override Staff.HorizontalBracketText.text = "inférieur"
    d'\startGroup e' fis' g'\stopGroup
    \once \override Staff.HorizontalBracketText.text = "supérieur"
    a'\startGroup b' \tweak color #(rgb-color 0.588 0.157 0.118) \tweak Stem.color #(rgb-color 0.588 0.157 0.118) cis'' d''\stopGroup
    \bar "" \break
    \set Staff.shortInstrumentName = \markup \small "la"
    \once \override Staff.KeySignature.stencil = #(armure-nouveau-signe 4 (rgb-color 0.588 0.157 0.118))
    \key a \major
    \once \override Staff.HorizontalBracketText.text = "inférieur"
    a\startGroup b cis' d'\stopGroup
    \once \override Staff.HorizontalBracketText.text = "supérieur"
    e'\startGroup fis' \tweak color #(rgb-color 0.588 0.157 0.118) \tweak Stem.color #(rgb-color 0.588 0.157 0.118) gis' a'\stopGroup
    \bar "" \break
    \set Staff.shortInstrumentName = \markup \small "mi"
    \once \override Staff.KeySignature.stencil = #(armure-nouveau-signe 1 (rgb-color 0.588 0.157 0.118))
    \key e \major
    \once \override Staff.HorizontalBracketText.text = "inférieur"
    e'\startGroup fis' gis' a'\stopGroup
    \once \override Staff.HorizontalBracketText.text = "supérieur"
    b'\startGroup cis'' \tweak color #(rgb-color 0.588 0.157 0.118) \tweak Stem.color #(rgb-color 0.588 0.157 0.118) dis'' e''\stopGroup
    \bar "" \break
    \set Staff.shortInstrumentName = \markup \small "si"
    \once \override Staff.KeySignature.stencil = #(armure-nouveau-signe 5 (rgb-color 0.588 0.157 0.118))
    \key b \major
    \once \override Staff.HorizontalBracketText.text = "inférieur"
    b\startGroup cis' dis' e'\stopGroup
    \once \override Staff.HorizontalBracketText.text = "supérieur"
    fis'\startGroup gis' \tweak color #(rgb-color 0.588 0.157 0.118) \tweak Stem.color #(rgb-color 0.588 0.157 0.118) ais' b'\stopGroup
    \bar "" \break
    \set Staff.shortInstrumentName = \markup \small "fa dièse"
    \once \override Staff.KeySignature.stencil = #(armure-nouveau-signe 2 (rgb-color 0.588 0.157 0.118))
    \key fis \major
    \once \override Staff.HorizontalBracketText.text = "inférieur"
    fis'\startGroup gis' ais' b'\stopGroup
    \once \override Staff.HorizontalBracketText.text = "supérieur"
    cis''\startGroup dis'' \tweak color #(rgb-color 0.588 0.157 0.118) \tweak Stem.color #(rgb-color 0.588 0.157 0.118) eis'' fis''\stopGroup
    \bar "" \break
    \set Staff.shortInstrumentName = \markup \small "do dièse"
    \once \override Staff.KeySignature.stencil = #(armure-nouveau-signe 6 (rgb-color 0.588 0.157 0.118))
    \key cis \major
    \once \override Staff.HorizontalBracketText.text = "inférieur"
    cis'\startGroup dis' eis' fis'\stopGroup
    \once \override Staff.HorizontalBracketText.text = "supérieur"
    gis'\startGroup ais' \tweak color #(rgb-color 0.588 0.157 0.118) \tweak Stem.color #(rgb-color 0.588 0.157 0.118) bis' cis''\stopGroup
    \bar "|."
  }
  \layout {
    indent = 18\mm
    short-indent = 18\mm
    \context {
      \Score
      \override SpacingSpanner.base-shortest-duration = #(ly:make-moment 1/2)
      \override SpacingSpanner.spacing-increment = #2.2
    }
  }
}
