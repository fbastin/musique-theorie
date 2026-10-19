\version "2.24.3"
%% Fichier produit par outils/generer_mesure.py — ne pas modifier à la main.
\paper {
  indent = 0
  paper-width = 152\mm
  line-width = 150\mm
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
  \new Staff { \new Voice {
        \clef treble \autoBeamOff \numericTimeSignature \textLengthOn
        \time 2/4 r8 c''8^\markup \tiny \italic "contretemps" r8 d''8^\markup \tiny \italic "contretemps" | r4 e''4^\markup \tiny \italic "contretemps" | r8 f''8^\markup \tiny \italic "contretemps" g''4 | c''2
        \bar "|."
      } }
  \layout {
    \context { \Score \override SpacingSpanner.spacing-increment = #1.6 \omit BarNumber }
  }
}
