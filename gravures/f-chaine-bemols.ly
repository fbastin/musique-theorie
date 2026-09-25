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
    \set Staff.shortInstrumentName = \markup \small "fa"
    \once \override Staff.KeySignature.stencil = #(armure-nouveau-signe 6 (rgb-color 0.588 0.157 0.118))
    \key f \major
    \once \override Staff.HorizontalBracketText.text = "inférieur"
    f'\startGroup g' a' \tweak color #(rgb-color 0.588 0.157 0.118) \tweak Stem.color #(rgb-color 0.588 0.157 0.118) bes'\stopGroup
    \once \override Staff.HorizontalBracketText.text = "supérieur"
    c''\startGroup d'' e'' f''\stopGroup
    \bar "" \break
    \set Staff.shortInstrumentName = \markup \small "si bémol"
    \once \override Staff.KeySignature.stencil = #(armure-nouveau-signe 2 (rgb-color 0.588 0.157 0.118))
    \key bes \major
    \once \override Staff.HorizontalBracketText.text = "inférieur"
    bes\startGroup c' d' \tweak color #(rgb-color 0.588 0.157 0.118) \tweak Stem.color #(rgb-color 0.588 0.157 0.118) ees'\stopGroup
    \once \override Staff.HorizontalBracketText.text = "supérieur"
    f'\startGroup g' a' bes'\stopGroup
    \bar "" \break
    \set Staff.shortInstrumentName = \markup \small "mi bémol"
    \once \override Staff.KeySignature.stencil = #(armure-nouveau-signe 5 (rgb-color 0.588 0.157 0.118))
    \key ees \major
    \once \override Staff.HorizontalBracketText.text = "inférieur"
    ees'\startGroup f' g' \tweak color #(rgb-color 0.588 0.157 0.118) \tweak Stem.color #(rgb-color 0.588 0.157 0.118) aes'\stopGroup
    \once \override Staff.HorizontalBracketText.text = "supérieur"
    bes'\startGroup c'' d'' ees''\stopGroup
    \bar "" \break
    \set Staff.shortInstrumentName = \markup \small "la bémol"
    \once \override Staff.KeySignature.stencil = #(armure-nouveau-signe 1 (rgb-color 0.588 0.157 0.118))
    \key aes \major
    \once \override Staff.HorizontalBracketText.text = "inférieur"
    aes\startGroup bes c' \tweak color #(rgb-color 0.588 0.157 0.118) \tweak Stem.color #(rgb-color 0.588 0.157 0.118) des'\stopGroup
    \once \override Staff.HorizontalBracketText.text = "supérieur"
    ees'\startGroup f' g' aes'\stopGroup
    \bar "" \break
    \set Staff.shortInstrumentName = \markup \small "ré bémol"
    \once \override Staff.KeySignature.stencil = #(armure-nouveau-signe 4 (rgb-color 0.588 0.157 0.118))
    \key des \major
    \once \override Staff.HorizontalBracketText.text = "inférieur"
    des'\startGroup ees' f' \tweak color #(rgb-color 0.588 0.157 0.118) \tweak Stem.color #(rgb-color 0.588 0.157 0.118) ges'\stopGroup
    \once \override Staff.HorizontalBracketText.text = "supérieur"
    aes'\startGroup bes' c'' des''\stopGroup
    \bar "" \break
    \set Staff.shortInstrumentName = \markup \small "sol bémol"
    \once \override Staff.KeySignature.stencil = #(armure-nouveau-signe 0 (rgb-color 0.588 0.157 0.118))
    \key ges \major
    \once \override Staff.HorizontalBracketText.text = "inférieur"
    ges'\startGroup aes' bes' \tweak color #(rgb-color 0.588 0.157 0.118) \tweak Stem.color #(rgb-color 0.588 0.157 0.118) ces''\stopGroup
    \once \override Staff.HorizontalBracketText.text = "supérieur"
    des''\startGroup ees'' f'' ges''\stopGroup
    \bar "" \break
    \set Staff.shortInstrumentName = \markup \small "do bémol"
    \once \override Staff.KeySignature.stencil = #(armure-nouveau-signe 3 (rgb-color 0.588 0.157 0.118))
    \key ces \major
    \once \override Staff.HorizontalBracketText.text = "inférieur"
    ces'\startGroup des' ees' \tweak color #(rgb-color 0.588 0.157 0.118) \tweak Stem.color #(rgb-color 0.588 0.157 0.118) fes'\stopGroup
    \once \override Staff.HorizontalBracketText.text = "supérieur"
    ges'\startGroup aes' bes' ces''\stopGroup
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
