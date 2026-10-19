\version "2.24.3"
%% Fichier produit par outils/generer_tonalites.py — ne pas modifier à la main.
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
    \set Staff.instrumentName = \markup \small "do majeur"
    \key c \major
    c'_\markup \small \bold "1" d'_\markup \small "2" \tweak color #(rgb-color 0.588 0.157 0.118) \tweak Stem.color #(rgb-color 0.588 0.157 0.118) \tweak Accidental.color #(rgb-color 0.588 0.157 0.118) e'_\markup \small \with-color #(rgb-color 0.588 0.157 0.118) "3" f'_\markup \small \bold "4" g'_\markup \small \bold "5" \tweak color #(rgb-color 0.588 0.157 0.118) \tweak Stem.color #(rgb-color 0.588 0.157 0.118) \tweak Accidental.color #(rgb-color 0.588 0.157 0.118) a'_\markup \small \with-color #(rgb-color 0.588 0.157 0.118) "6" b'_\markup \small "7" c''
    \bar "" \break
    \set Staff.shortInstrumentName = \markup \small "do mineur"
    \key c \minor
    c'_\markup \small \bold "1" d'_\markup \small "2" \tweak color #(rgb-color 0.588 0.157 0.118) \tweak Stem.color #(rgb-color 0.588 0.157 0.118) \tweak Accidental.color #(rgb-color 0.588 0.157 0.118) ees'_\markup \small \with-color #(rgb-color 0.588 0.157 0.118) "3" f'_\markup \small \bold "4" g'_\markup \small \bold "5" \tweak color #(rgb-color 0.588 0.157 0.118) \tweak Stem.color #(rgb-color 0.588 0.157 0.118) \tweak Accidental.color #(rgb-color 0.588 0.157 0.118) aes'_\markup \small \with-color #(rgb-color 0.588 0.157 0.118) "6" b'_\markup \small "7" c''
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
